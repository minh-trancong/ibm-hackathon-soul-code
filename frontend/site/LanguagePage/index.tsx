import { useState } from "react";
import { useRouter } from "next/router";
import Layout from "@/components/Layout";
import Icon from "@/components/Icon";

const data = [
    {
        word: 'Rocket Memory',
        meaning: 'Techniques to improve learning and memory retention',
        example: 'Using Rocket Memory techniques can enhance your ability to remember music and public speaking.',
        relatedDocs: ['Learning Music Through Relaxation, Active Learning, and Memory Consolidation: A Study on Rocket Memory Techniques and Their Benefits for Public Speaking and Music Appreciation']
    },
    {
        word: 'Relaxation',
        meaning: 'The state of being free from tension and anxiety',
        example: 'Listening to music in a relaxed state can improve memory retention.',
        relatedDocs: ['Learning Music Through Relaxation, Active Learning, and Memory Consolidation: A Study on Rocket Memory Techniques and Their Benefits for Public Speaking and Music Appreciation']
    },
    {
        word: 'Active Learning',
        meaning: 'Learning method that involves actively engaging with the material',
        example: 'Engaging in active learning strategies can enhance memory recall.',
        relatedDocs: ['Learning Music Through Relaxation, Active Learning, and Memory Consolidation: A Study on Rocket Memory Techniques and Their Benefits for Public Speaking and Music Appreciation']
    },
    {
        word: 'Memory Consolidation',
        meaning: 'The process of stabilizing a memory trace after the initial acquisition',
        example: 'Consolidating memories through repetition can improve recall.',
        relatedDocs: ['Learning Music Through Relaxation, Active Learning, and Memory Consolidation: A Study on Rocket Memory Techniques and Their Benefits for Public Speaking and Music Appreciation']
    },
    {
        word: 'Memory Retention',
        meaning: 'The ability to retain information over time',
        example: 'Techniques that enhance memory retention are beneficial for learning.',
        relatedDocs: ['Learning Music Through Relaxation, Active Learning, and Memory Consolidation: A Study on Rocket Memory Techniques and Their Benefits for Public Speaking and Music Appreciation']
    },
    {
        word: 'Recall',
        meaning: 'The act of retrieving information from memory',
        example: 'These techniques can improve your ability to recall information.',
        relatedDocs: ['Learning Music Through Relaxation, Active Learning, and Memory Consolidation: A Study on Rocket Memory Techniques and Their Benefits for Public Speaking and Music Appreciation']
    },
    {
        word: 'Public Speaking',
        meaning: 'The act of performing a speech to a live audience',
        example: 'Individuals who struggle with public speaking can benefit from these techniques.',
        relatedDocs: ['Learning Music Through Relaxation, Active Learning, and Memory Consolidation: A Study on Rocket Memory Techniques and Their Benefits for Public Speaking and Music Appreciation']
    },
    {
        word: 'Music Appreciation',
        meaning: 'The understanding and enjoyment of music',
        example: 'These techniques can help with music appreciation.',
        relatedDocs: ['Learning Music Through Relaxation, Active Learning, and Memory Consolidation: A Study on Rocket Memory Techniques and Their Benefits for Public Speaking and Music Appreciation']
    },
    {
        word: 'Repetition',
        meaning: 'The action of repeating something that has already been said or written',
        example: 'Consolidating memories through repetition can improve recall.',
        relatedDocs: ['Learning Music Through Relaxation, Active Learning, and Memory Consolidation: A Study on Rocket Memory Techniques and Their Benefits for Public Speaking and Music Appreciation']
    },
    {
        word: 'Study Routine',
        meaning: 'A regular schedule of study activities',
        example: 'Incorporating these techniques into your study routine can lead to significant improvements.',
        relatedDocs: ['Learning Music Through Relaxation, Active Learning, and Memory Consolidation: A Study on Rocket Memory Techniques and Their Benefits for Public Speaking and Music Appreciation']
    }
];
const LanguagePage = () => {
    const [search, setSearch] = useState<string>("");
    const router = useRouter();

    return (
        <Layout hideRightSidebar>
            <div className="p-10 md:pt-5 md:px-6 md:pb-10">
                <button
                    className="hidden absolute top-6 right-6 w-10 h-10 border-2 border-n-4/25 rounded-full text-0 transition-colors hover:border-transparent hover:bg-n-4/25 md:block"
                    onClick={() => router.back()}
                >
                    <Icon className="fill-n-4" name="close"/>
                </button>
                <div className="h3 leading-[4rem] md:mb-3 md:h3">
                    Welcome to Language Page!
                </div>
                <div className="mb-8 body1 text-n-4 md:mb-6 md:body1S">
                    Explore and learn different programming languages
                </div>
                <div className="mb-11 h6 text-n-4 md:mb-6">Available Languages</div>
                <div className="flex flex-wrap -mx-7 -mt-16 2xl:-mx-4 2xl:-mt-12 md:block md:mt-0 md:mx-0">
                </div>
                <table className="min-w-full bg-white border border-gray-200">
                    <thead>
                    <tr>
                        <th className="py-2 px-4 border-b">English Word</th>
                        <th className="py-2 px-4 border-b">Meaning</th>
                        <th className="py-2 px-4 border-b">Example</th>
                        <th className="py-2 px-4 border-b">Related Documents</th>
                    </tr>
                    </thead>
                    <tbody>
                    {data.map((item, index) => (
                        <tr key={index}>
                            <td className="py-2 px-4 border-b">{item.word}</td>
                            <td className="py-2 px-4 border-b">{item.meaning}</td>
                            <td className="py-2 px-4 border-b">{item.example}</td>
                            <td className="py-2 px-4 border-b">
                                {item.relatedDocs.join(', ')}
                            </td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            </div>
        </Layout>
    );
};

export default LanguagePage;