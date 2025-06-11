'use client';

import { useState, Suspense } from 'react';
import { Input } from '@/components/ui/input';
import { ApiResponse } from '@/util/types';
import { useQuery } from '@tanstack/react-query';
import { ChartAreaInteractive } from '@/components/chart-area-interactive';

const fetchProduct = async (product: string): Promise<ApiResponse[]> => {
    const res = await fetch(`http://localhost:8000/api/product/${product}`);
    if (!res.ok) throw new Error('Failed to fetch product data');
    return res.json();
};

export default function Dashboard() {
    const [product, setProduct] = useState('ENCHANTED_DIAMOND');

    const { data, isLoading, isError } = useQuery({
        queryKey: ['product', product],
        queryFn: () => fetchProduct(product),
        refetchInterval: 600_000, // 10 minutes
    });

    return (
        <main className="p-6 grid gap-6">
            <Input placeholder="Enter product key..." value={product} onChange={(e) => setProduct(e.target.value)} />
            {isLoading && <p>Loading chart…</p>}
            {isError && <p>Error loading data.</p>}
            {data && <ChartAreaInteractive productData={data} />}
        </main>
    );
}
