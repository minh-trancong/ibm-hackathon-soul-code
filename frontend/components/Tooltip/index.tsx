// frontend/components/Tooltip/index.tsx
import { ReactNode } from "react";

type TooltipProps = {
    text: string;
    children: ReactNode;
};

const Tooltip = ({ text, children }: TooltipProps) => {
    return (
        <div className="relative group">
            {children}
            <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 hidden group-hover:block bg-black text-white text-xs rounded py-1 px-2">
                {text}
            </div>
        </div>
    );
};

export default Tooltip;