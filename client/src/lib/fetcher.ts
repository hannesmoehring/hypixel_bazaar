export async function fetchJson<T>(url: string): Promise<T> {
    const r = await fetch(url, { next: { revalidate: 0 } });
    if (!r.ok) throw new Error(`API ${r.status}`);
    return r.json();
}
