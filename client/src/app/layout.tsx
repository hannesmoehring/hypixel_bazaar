import './globals.css';
import Providers from './providers';

export const metadata = {
    title: 'BZ-Dash',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
    return (
        <html lang="en">
            <body className="min-h-screen">
                <Providers>
                    <div className="mx-auto max-w-6xl px-4 py-6">{children}</div>
                </Providers>
            </body>
        </html>
    );
}
