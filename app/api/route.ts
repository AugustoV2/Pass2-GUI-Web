

import { NextRequest, NextResponse } from 'next/server';


interface RequestBody {
    code: string; 
}


interface ResponseResult {
    intermediate_file: string[];
    symtab: Record<string, string | number>; 
    object_code: string[];
}

export async function POST(req: NextRequest) {
    try {
       
        const body: RequestBody = await req.json();
        const inputFileContent = body.code;

      
        const result = await runCode(inputFileContent);

      
        if ('error' in result) {
            return NextResponse.json(result, { status: 500 }); // Return error response
        }

       
        return NextResponse.json(result as ResponseResult, { status: 200 });
    } catch (error) {
       
        return NextResponse.json({ error: (error as Error).message }, { status: 500 });
    }
}


async function runCode(inputFileContent: string): Promise<ResponseResult | { error: string }> {
    try {
        const response = await fetch('https://running-krill-augustov-d8e56e16.koyeb.app/pass1', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                code: inputFileContent,
            }),
        });

        
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

     
        const result: ResponseResult = await response.json();
        console.log('Response from server:', result);
        return result;
    } catch (error) {
        console.error('Error:', error);
        return { error: (error as Error).message }; // Return error as an object
    }
}
