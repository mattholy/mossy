import { defineConfig } from '@hey-api/openapi-ts';

export default defineConfig({
    client: 'fetch',
    format: 'prettier',
    lint: 'eslint',
    input: 'http://localhost:8000/openapi.json',
    output: 'src/client',
    types: {
        enums: 'typescript',
    },
});
