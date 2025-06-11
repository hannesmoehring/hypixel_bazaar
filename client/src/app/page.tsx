import Link from 'next/link';
import { Button } from '@/components/ui/button';

export default function Home() {
    return (
        <main className="flex flex-col items-center justify-start min-h-screen px-4 pt-50">
            <h1 className="text-3xl md:text-5xl font-bold text-center mb-6">
                Computational Approaches to In-Game Bazaar Analysis
            </h1>
            <p className="max-w-2xl text-center text-muted-foreground mb-10 pt-8">
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et
                dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip
                ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu
                fugiat nulla pariatur.
                <br />
                <a
                    href="https://github.com/your-username/your-repo"
                    className="underline text-blue-600 hover:text-blue-800"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    View on GitHub
                </a>
            </p>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-5 w-full max-w-md pt-10">
                <Link href="/quick-overview">
                    <Button className="w-full">Quick Overview</Button>
                </Link>
                <Link href="/general-ranking">
                    <Button className="w-full">General Ranking</Button>
                </Link>
                <Link href="/advanced">
                    <Button className="w-full">Advanced Information</Button>
                </Link>
                <Link href="/ai-prediction">
                    <Button className="w-full">AI Prediction</Button>
                </Link>
            </div>
        </main>
    );
}
