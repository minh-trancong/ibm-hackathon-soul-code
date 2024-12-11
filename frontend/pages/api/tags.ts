// `pages/api/tags.ts`

import { NextApiRequest, NextApiResponse } from 'next';

const tags = ['Tag1', 'Tag2', 'Tag3', 'Tag4', 'Tag5'];

export default function handler(req: NextApiRequest, res: NextApiResponse) {
    res.status(200).json(tags);
}