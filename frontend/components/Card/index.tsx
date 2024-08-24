import React from "react";

type DocumentType = {
    image: string;
    title: string;
    summary: string;
    tags: string[];
};

type CardProps = {
    document: DocumentType;
};

const Card = ({ document }: CardProps) => (
    <div className="md:w-1/3 p-4 box-border relative group">
        <div className="relative p-6 bg-white border border-gray-300 rounded-lg transition-shadow duration-300 hover:shadow-md dark:bg-gray-800">
            <div className="flex flex-col mb-2 md:mb-6">
                <img src={document.image} alt={document.title} className="w-full h-32 object-cover mb-4" />
                <h2 className="text-left font-bold">{document.title}</h2>
            </div>
            <p className="mb-4 text-gray-600 dark:text-gray-400">{document.summary}</p>
            <div className="flex flex-wrap gap-2">
                {document.tags.map((tag, index) => (
                    <span key={index} className="bg-blue-500 text-white px-2 py-1 rounded text-sm">
                        #{tag}
                    </span>
                ))}
            </div>
        </div>
        <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300">
            <button className="btn-overlay mx-2">View</button>
            <button className="btn-overlay mx-2">Review</button>
            <button className="btn-overlay mx-2">Ask</button>
        </div>
    </div>
);

export default Card;