import { useState } from "react";
import Layout from "@/components/Layout";
import Chat from "@/components/Chat";
import Message from "@/components/Message";
import Question from "@/components/Question";
import Answer from "@/components/Answer";
import { format } from "date-fns";
import Feedback from "@/components/Feedback";
import RecentDocumentsSidebar from "@/components/RecentDocumentsSidebar";

type ChatMessage = {
    type: 'question' | 'answer';
    content: string | JSX.Element;
};

const ActiveRecallPage = () => {
    const [message, setMessage] = useState<string>("");
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [chat, setChat] = useState<ChatMessage[]>([]); // New state for storing both questions and answers

    const handleSubmit = async () => {
        setIsLoading(true);
        setChat([...chat, { type: 'question', content: message }]); // Add the new question to the chat

        const response = await fetch('http://34.143.149.236:443/api/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: message }),
        });

        const data = await response.json();

        // Create a string with the response and the links
        let content = data.response;
        data.selected_fields.forEach((link: string, index: number) => {
            content += `<br/>[${index + 1}] - <a href="${link}" target="_blank" rel="noopener noreferrer" style="color: blue;">${link}</a>`;
        });

        // Add the new response to the chat
        setChat([...chat, { type: 'question', content: message }, { type: 'answer', content: <div dangerouslySetInnerHTML={{ __html: content }} /> }]);
        setIsLoading(false);
    };

    const currentDate = format(new Date(), 'dd/MM/yyyy');

    return (
        <Layout showRecentDocumentSideBar>
            <Chat title={`Test your knowledge - @Today(${currentDate})`}>
                {chat.map((item, index) => item.type === 'question' ?
                    <Question key={index} content={item.content} time="Just now" /> :
                    <Answer key={index} time="Just now">{item.content}</Answer>
                )}
                {isLoading && <Answer loading />}
            </Chat>
            <Message
                value={message}
                onChange={(e: any) => setMessage(e.target.value)}
                onButtonClick={handleSubmit} // Pass handleSubmit as the onButtonClick prop
            />
        </Layout>
    );
};

export default ActiveRecallPage;