import { Suspense } from 'react';
import { PriceChart } from '@/components/PriceChart';

export default function Dashboard() {
  return (
    <main className="p-6 grid gap-6">
      <Suspense fallback={<p>Loading chart…</p>}>
        <PriceChart product="ENCHANTED_DIAMOND" />
      </Suspense>
    </main>
  );
}