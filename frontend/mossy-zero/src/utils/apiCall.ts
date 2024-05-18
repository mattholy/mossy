import pinia from '@/stores';
import { useUserStateStore } from '@/stores/userStateStore';

interface FetchOptions {
    endpoint: string;
    data?: any;
}

interface MossyApiResponse {
    status: string;
    msg: string;
    payload: any;
}

const baseUrl = import.meta.env.VITE_BASE_URL || ''

export async function callMossyApi({ endpoint, data }: FetchOptions): Promise<any> {
    if (!endpoint.startsWith('/')) {
        throw new Error('Endpoint must start with /');
    }
    if (!isValidJson(data)) {
        throw new Error("Provided data is not a valid JSON object.");
    }
    const userStateStore = useUserStateStore(pinia);
    const headers = new Headers({
        'Content-Type': 'application/json',
        'X-Mossy-API': 'api/m1',
    });

    if (userStateStore.isLoggedIn) {
        headers.append('Authorization', `Bearer ${userStateStore.currentToken}`);
    }

    const fetchOptions: RequestInit = {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(data)
    };
    const response = await fetch(`${baseUrl}${endpoint}`, fetchOptions);

    const responseData: MossyApiResponse = await response.json()

    if (responseData.status === 'OK') {
        return responseData.payload
    } else {
        throw new MossyApiError(responseData.status, responseData.msg, responseData.payload)
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

export class MossyApiError extends Error {
    public type: string;
    public category: string;
    public detail: string;

    constructor(type: string, category: string, detail: string) {
        super(`[${type}]: ${category} - ${detail}`);
        this.name = 'MossyApiError';
        this.type = type;
        this.category = category;
        this.detail = detail;
        Object.setPrototypeOf(this, MossyApiError.prototype);
    }

    displayError() {
        return `Error Type: ${this.type}, Category: ${this.category}, Details: ${this.detail}`;
    }
}
