import { useAuthStore } from '@/stores/AuthStore';

interface FetchOptions {
    endpoint: string;
    data?: any;
}

const baseUrl = import.meta.env.VITE_BASE_URL || ''

export async function callMossyApi({ endpoint, data }: FetchOptions): Promise<any> {
    if (!endpoint.startsWith('/')) {
        throw new Error('Endpoint must start with /');
    }
    if (!isValidJson(data)) {
        throw new Error("Provided data is not a valid JSON object.");
    }
    const store = useAuthStore();
    const headers = new Headers({
        'Content-Type': 'application/json',
        'X-Mossy-API': 'api/m1',
    });

    if (store.token) {
        headers.append('Authorization', `Bearer ${store.token}`);
    }

    const fetchOptions: RequestInit = {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(data)
    };
    const response = await fetch(`${baseUrl}/api${endpoint}`, fetchOptions);

    const responseData = await response.json()

    if (responseData.status === 'OK') {
        return responseData.payload
    } else {
        if (responseData.status === 'SERVER_ERROR') {
            throw new Error(responseData.msg)
        } else {
            throw new Error(responseData.payload)
        }
    }
}

function isValidJson(data: any): boolean {
    try {
        JSON.stringify(data);
        return true;
    } catch (e) {
        return false;
    }
}