import { useState } from 'react';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement } from 'chart.js';
import { Bar } from 'react-chartjs-2';
import { jStat } from 'jstat';

ChartJS.register(CategoryScale, LinearScale, BarElement);

export default function Home() {
  const [distType, setDistType] = useState('Normal');
  const [mean, setMean] = useState(100);
  const [sd, setSd] = useState(10);
  const [alpha, setAlpha] = useState(2);
  const [beta, setBeta] = useState(2);
  const [samples, setSamples] = useState([]);

  function generateSamples() {
    const n = 1000;
    const arr = [];
    for (let i = 0; i < n; i++) {
      if (distType === 'Normal') {
        arr.push(jStat.normal.sample(mean, sd));
      } else if (distType === 'Beta') {
        arr.push(jStat.beta.sample(alpha, beta));
      }
    }
    setSamples(arr);
  }

  const histData = (() => {
    if (!samples.length) return null;
    const bins = 20;
    const min = Math.min(...samples);
    const max = Math.max(...samples);
    const width = (max - min) / bins;
    const counts = Array(bins).fill(0);
    samples.forEach(value => {
      const idx = Math.min(
        bins - 1,
        Math.floor((value - min) / width)
      );
      counts[idx] += 1;
    });
    return {
      labels: counts.map((_, i) => (min + i * width).toFixed(1)),
      datasets: [
        {
          label: 'Frequency',
          data: counts,
          backgroundColor: 'rgba(75,192,192,0.6)'
        }
      ]
    };
  })();

  return (
    <div>
      <h1>Probabilistic Revenue Simulator</h1>
      <div style={{ display: 'flex', gap: '1rem', marginBottom: '1rem' }}>
        <label>
          Distribution
          <select value={distType} onChange={e => setDistType(e.target.value)}>
            <option value="Normal">Normal</option>
            <option value="Beta">Beta</option>
          </select>
        </label>
        {distType === 'Normal' && (
          <>
            <label>
              Mean
              <input type="number" value={mean} onChange={e => setMean(Number(e.target.value))} />
            </label>
            <label>
              Std Dev
              <input type="number" value={sd} onChange={e => setSd(Number(e.target.value))} />
            </label>
          </>
        )}
        {distType === 'Beta' && (
          <>
            <label>
              Alpha
              <input type="number" value={alpha} onChange={e => setAlpha(Number(e.target.value))} />
            </label>
            <label>
              Beta
              <input type="number" value={beta} onChange={e => setBeta(Number(e.target.value))} />
            </label>
          </>
        )}
        <button onClick={generateSamples}>Simulate</button>
      </div>
      {histData && <Bar data={histData} />}
    </div>
  );
}
