import Link from "next/link";
import Image from "@/components/Image";
import {DocumentType} from "../index";
import TagList from "@/components/TagList";

type ItemProps = {
    item: DocumentType;
};

const Item = ({ item }: ItemProps) => (
    <div className="">
        <div className="flex items-center py-3 md:pt-6">
            <Link
                className="group flex items-center w-full pl-5 py-5 pr-24 rounded-xl transition-colors hover:bg-n-3/50 md:!bg-transparent md:py-0 md:pl-0 md:pr-18 md:mb-6 md:last:mb-0 dark:hover:bg-n-6 dark:md:hover:bg-transparent"
                key={item.id}
                href={`/documents?id=${item.id}`}
            >
                <div className="flex flex-col ml-5 w-full">
                    <div className="h6">
                        {item.title ? (item.title.length > 30 ? item.title.substring(0, 90) + "..." : item.title) : ""}
                    </div>
                    <div className="caption1 text-n-4/75">
                        {item.summary ? (item.summary.length > 100 ? item.summary.substring(0, 200) + "..." : item.summary) : ""}
                    </div>
                    <TagList tags={item.tags} hideViewAll/>
                </div>
            </Link>
        </div>
    </div>
);

export default Item;