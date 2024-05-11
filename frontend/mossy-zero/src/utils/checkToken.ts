export async function checkToken(token: string): Promise<boolean> {
    const baseUrl = import.meta.env.VITE_BASE_URL || '';
    try {
        const response = await fetch(`${baseUrl}/api/m1/auth/verify-jwt`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: token
        });
        const data = await response.json();
        return response.ok && data.status === 'OK';
    } catch (error) {
        console.error('Error verifying token:', error);
        return false;
    }
}
