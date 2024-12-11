// frontend/components/RecentDocumentsSidebar/DocumentItem.tsx
import Link from "next/link";
import Icon from "@/components/Icon";
import Tooltip from "@/components/Tooltip";

type DocumentItemProps = {
    item: {
        id: string;
        title: string;
        date: string;
    };
};

const DocumentItem = ({ item }: DocumentItemProps) => {
    return (
        <div className="flex items-center p-4 border-b border-n-3 dark:border-n-5">
            <div className="ml-2 flex-grow">
                <div className="base1 font-semibold dark:text-n-1">{item.title}</div>
                <div className="caption1 text-n-4/75 dark:text-n-4/50">{item.date}</div>
            </div>
            <Tooltip text="Test">
                <Link href={`/documents/${item.id}`} className="ml-2">
                    <button className="btn-icon">
                        <Icon name="test-icon" className="w-6 h-6 fill-n-4" />
                    </button>
                </Link>
            </Tooltip>
            <Tooltip text="View File">
                <Link href={`/documents/${item.id}`} className="ml-2">
                    <button className="btn-icon">
                        <Icon name="arrow-next" className="w-6 h-6 fill-n-4" />
                    </button>
                </Link>
            </Tooltip>
        </div>
    );
};

export default DocumentItem;