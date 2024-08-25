import React, { useState } from "react";
import { useRouter } from "next/router";
import Layout from "@/components/Layout";
import Icon from "@/components/Icon";
import axios from "axios";
import { API_ENDPOINTS } from "@/utils/apiConfig";
import Modal from "@/components/Modal"; // Import the Modal component

const UploadDocumentPage = () => {
    const [link, setLink] = useState<string>("");
    const [files, setFiles] = useState<File[]>([]);
    const [modalVisible, setModalVisible] = useState<boolean>(false);
    const [modalMessage, setModalMessage] = useState<string>("");
    const router = useRouter();

    const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
        event.preventDefault();
        const newFiles = Array.from(event.dataTransfer.files);
        setFiles((prevFiles) => [...prevFiles, ...newFiles]);
    };

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const newFiles = Array.from(event.target.files || []);
        setFiles((prevFiles) => [...prevFiles, ...newFiles]);
    };

    const handleLinkChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setLink(event.target.value);
    };

    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        const formData = new FormData();
        files.forEach((file) => {
            formData.append("file", file);
        });

        try {
            const response = await axios.post(API_ENDPOINTS.UPLOAD_DOCUMENT, formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            });
            setModalMessage("Document uploaded successfully!");
            setModalVisible(true);
        } catch (error) {
            setModalMessage("Error uploading document.");
            setModalVisible(true);
        }
    };

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
                    Upload Document
                </div>
                <div className="mb-8 body1 text-n-4 md:mb-6 md:body1S">
                    Upload your documents by dragging and dropping files or by entering a link.
                </div>
                <form onSubmit={handleSubmit}>
                    <div
                        className="border-2 border-dashed border-n-4/25 p-6 mb-6"
                        onDrop={handleDrop}
                        onDragOver={(e) => e.preventDefault()}
                    >
                        <p className="text-center text-n-4">Drag and drop your files here</p>
                        <input
                            type="file"
                            multiple
                            className="hidden"
                            onChange={handleFileChange}
                        />
                    </div>
                    <div className="text-center my-4 text-n-4">OR</div>
                    <div className="mb-6">
                        <input
                            type="text"
                            value={link}
                            onChange={handleLinkChange}
                            placeholder="Enter a link (video or audio)"
                            className="w-full p-2 border border-n-4/25 rounded"
                        />
                    </div>
                    <div className="flex flex-wrap -mx-4">
                        {files.map((file, index) => (
                            <div key={index} className="p-4">
                                <p>{file.name}</p>
                            </div>
                        ))}
                    </div>
                    <button
                        type="submit"
                        className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-700"
                    >
                        Submit
                    </button>
                </form>
            </div>
            <Modal visible={modalVisible} onClose={() => setModalVisible(false)}>
                {modalMessage}
            </Modal>
        </Layout>
    );
};

export default UploadDocumentPage;