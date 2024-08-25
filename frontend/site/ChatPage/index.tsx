import { useState } from "react";
import Layout from "@/components/Layout";
import Chat from "@/components/Chat";
import Message from "@/components/Message";
import Question from "@/components/Question";
import Answer from "@/components/Answer";
import { format } from "date-fns";
import Feedback from "@/components/Feedback";
import RecentDocumentsSidebar from "@/components/RecentDocumentsSidebar";
import { API_ENDPOINTS } from "@/utils/apiConfig";

type ChatMessage = {
    type: 'question' | 'answer';
    content: string | JSX.Element;
};

const ChatPage = () => {
    const [message, setMessage] = useState<string>("");
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [chat, setChat] = useState<ChatMessage[]>([]);

    const handleSubmit = async () => {
        setIsLoading(true);
        setChat([...chat, { type: 'question', content: message }]);

        const response = await fetch(API_ENDPOINTS.CHAT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message }),
        });

        let data = await response.text();
        data = data.replace(/\n/g, '<br>');

        setChat([...chat, { type: 'question', content: message }, { type: 'answer', content: <div dangerouslySetInnerHTML={{ __html: data }} /> }]);
        setIsLoading(false);
    };

    const currentDate = format(new Date(), 'dd/MM/yyyy');

    return (
        <Layout showRecentDocumentSideBar>
            <Chat title="Chat with your documents">
                {chat.map((item, index) => item.type === 'question' ?
                    <Question key={index} content={item.content} time="Just now" /> :
                    <Answer key={index} time="Just now">{item.content}</Answer>
                )}
                {isLoading && <Answer loading />}
            </Chat>
            <Message
                value={message}
                onChange={(e: any) => setMessage(e.target.value)}
                onButtonClick={handleSubmit}
            />
        </Layout>
    );
};

export default ChatPage;