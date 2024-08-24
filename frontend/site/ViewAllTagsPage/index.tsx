// `pages/ViewAllTagsPage.tsx`

import React, {useEffect, useState} from 'react';
import Layout from '@/components/Layout';
import axios from 'axios';

const ViewAllTagsPage = () => {
    const [tags, setTags] = useState<string[]>([]);

    useEffect(() => {
        // Fetch tags from an API or static source
        const fetchTags = async () => {
            try {
                const response = await axios.get('/api/tags');
                setTags(response.data);
            } catch (error) {
                console.error('Error fetching tags:', error);
            }
        };

        fetchTags();
    }, []);

    return (
        <Layout hideRightSidebar>
            <div className="p-4 md:pt-2 md:px-3 md:pb-4">
                <h1 className="h3 leading-10 md:mb-2 md:h3">All Tags</h1>
                <div className="mb-8 body1 text-n-4 md:mb-6 md:body1S">
                    Click to each tag and see your related documents
                </div>
                <div className="flex flex-wrap gap-2">
                    {tags.map((tag, index) => (
                        <button key={index} className="p-2 border rounded shadow hover:bg-blue-500 hover:text-white">
                            #{tag}
                        </button>
                    ))}
                </div>
            </div>
        </Layout>
    );
};

export default ViewAllTagsPage;