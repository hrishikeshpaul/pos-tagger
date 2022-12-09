import { AxiosResponse } from 'axios';

import { Http } from 'util/Http';

export interface Tag {
    prob: number;
    tag: string;
    word: string;
}

export const getTags = async (sentence: string): Promise<Tag[]> => {
    const { data }: AxiosResponse<Tag[]> = await Http.post('/', { sentence });

    return data;
};

export const getHealth = async (): Promise<string> => {
    const { data }: AxiosResponse<string> = await Http.get('/');

    return data;
};
