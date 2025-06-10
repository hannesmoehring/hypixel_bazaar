'use client';

import { useState, Suspense } from 'react';
import { PriceChart } from '@/components/PriceChart';
import { Input } from '@/components/ui/input';

export default function Dashboard() {
    const [product, setProduct] = useState('ENCHANTED_DIAMOND');

    return (
        <main className="p-6 grid gap-6">
            <Input placeholder="Enter product key..." value={product} onChange={(e) => setProduct(e.target.value)} />
            <Suspense fallback={<p>Loading chart…</p>}>
                <PriceChart product={product} />
            </Suspense>
        </main>
    );
}
