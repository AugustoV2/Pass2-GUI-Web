export async function runCode(inputFileContent: any) {
    try {
        const response = await fetch('http://127.0.0.1:5000/run-code', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                code: inputFileContent
            }),
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const result = await response.json();
        console.log('Response from server:', result); 
        return result;
    } catch (error) {
        console.error('Error:', error);
        return { error: (error as Error).message };
    }
}