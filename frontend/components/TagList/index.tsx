// frontend/components/TagList/index.tsx
import React from "react";
import { useRouter } from "next/router";

type TagListProps = {
    tags: string[];
    hideViewAll?: boolean; // New prop to control the visibility of "View All Tags"
};

const colors = ["#021526", "#03346E", "#F6B17A", "#A0153E"];

const getSequentialColor = (index: number) => colors[index % colors.length];

const TagList = ({ tags, hideViewAll = false }: TagListProps) => {
    const router = useRouter();

    const handleViewAllTags = () => {
        router.push("/view-all-tags");
    };

    return (
        <div className="grid grid-cols-10 gap-2 py-1">
            <div className="col-span-9 flex overflow-x-auto space-x-2 custom-scrollbar">
                {tags.map((tag, index) => (
                    <div
                        key={index}
                        className="px-2 py-1 rounded-md whitespace-nowrap text-sm text-white"
                        style={{ backgroundColor: getSequentialColor(index) }}
                    >
                        #{tag}
                    </div>
                ))}
            </div>
            {!hideViewAll && (
                <div className="col-span-1 flex items-center justify-center">
                    <button
                        className="px-2 py-1 rounded-md whitespace-nowrap font-bold bg-blue-500 text-white hover:shadow-lg"
                        onClick={handleViewAllTags}
                    >
                        View All Tags
                    </button>
                </div>
            )}
        </div>
    );
};

export default TagList;