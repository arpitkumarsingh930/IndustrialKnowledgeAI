import { useState } from "react";
import axios from "axios";

function UploadBox() {

    const [file, setFile] = useState(null);
    const [message, setMessage] = useState("");

    const handleUpload = async () => {

        if (!file) {
            alert("Please select a PDF first.");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        try {

            const response = await axios.post(
                "http://localhost:8080/api/documents/upload",
                formData,
                {
                    headers: {
                        "Content-Type": "multipart/form-data",
                    },
                }
            );

            setMessage("✅ Document uploaded successfully!");

            console.log(response.data);

        } catch (err) {

            console.error(err);

            setMessage("❌ Upload failed.");

        }

    };

    return (

        <div className="bg-slate-900 rounded-xl p-6">

            <h2 className="text-xl font-semibold mb-4">
                Upload PDF
            </h2>

            <input
                type="file"
                accept=".pdf"
                onChange={(e) => setFile(e.target.files[0])}
                className="mb-4 block w-full"
            />

            <button
                onClick={handleUpload}
                className="bg-cyan-500 hover:bg-cyan-600 px-5 py-2 rounded-lg font-semibold"
            >
                Upload
            </button>

            <p className="mt-4 text-green-400">
                {message}
            </p>

        </div>

    );

}

export default UploadBox;