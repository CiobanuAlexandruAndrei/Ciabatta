<template>
    <div class="container mx-auto p-4 bg-white rounded border-2">
        <div class="content-outline mb-6">
            <!-- Display the title dynamically as soon as it's available -->
            <h1 v-if="contentOutline.content_outline?.title" class="text-2xl font-bold mb-2">
                {{ contentOutline.content_outline.title }}
            </h1>

            <div class="mb-4">
                <!-- Target audience and "wrote as" fields -->
                <p v-if="contentOutline.content_outline?.target_audience" class="text-gray-700">
                    <strong>Target Audience:</strong> {{ contentOutline.content_outline.target_audience }}
                </p>
                <p v-if="contentOutline.content_outline?.wrote_as" class="text-gray-700">
                    <strong>Wrote As:</strong> {{ contentOutline.content_outline.wrote_as }}
                </p>
            </div>

            <div v-if="contentOutline.content_outline?.content" class="mb-4">                
                <!-- Access parsed JSON object values -->
                <p v-if="contentOutline.content_outline.content.metatags" class="text-gray-800">
                    <p class="text-gray-700"><h3 class="font-bold mt-3">URL</h3> {{ contentOutline.content_outline.content.metatags.url }}</p>
                    <p class="text-gray-700"><h3 class="font-bold mt-3">Page Title</h3> {{ contentOutline.content_outline.content.metatags.page_title }}</p>
                    <p class="text-gray-700"><h3 class="font-bold mt-3">Page Description</h3> {{ contentOutline.content_outline.content.metatags.page_description }}</p>
                </p>
                <br>
                <textarea class="min-h-[200px] text-gray-800 w-full border-blue-100 border-2 rounded-md h-full p-2">{{ contentOutline.content_outline.content.content.replaceAll('<br>', '\n') }}</textarea>
            </div> 
        </div>

        <!-- Display raw content as it's streaming in -->
        <div class="content-output">
            <h2 class="text-xl font-semibold mb-2">Raw Content Output</h2>
            <pre class="bg-gray-100 p-4 rounded border border-gray-300 overflow-x-auto">{{ rawContent }}</pre>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, defineProps } from "vue";
import { useRouter } from "vue-router";
import jsonAutocomplete from "json-autocomplete";
import { Input } from '@/components/ui/input';

// Define component props
const props = defineProps(["contentOutlineId"]);

// Initialize router
const router = useRouter();

// Define reactive variables
const contentOutlineId = ref("");
const contentOutline = ref({});
const content = ref("");  // Stores the final parsed content
const rawContent = ref("");  // Store raw streaming content

// Function to fetch content outline from API
async function fetchContentOutline() {
    const token = localStorage.getItem("token");

    try {
        const response = await fetch(
            `http://127.0.0.1:5000/api/get_content_outline/${contentOutlineId.value}`,
            {
                method: "GET",
                headers: {
                    Authorization: `Bearer ${token}`,
                    "Content-Type": "application/json",
                },
            }
        );

        if (!response.ok) {
            throw new Error("Network response was not ok");
        }

        // Reading the streamed response
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = ""; // Keep a buffer to store partial data

        while (true) {
            const { value, done } = await reader.read();
            if (done) break;

            // Decode the streamed chunk of data and append to buffer
            buffer += decoder.decode(value, { stream: true });

            try {
                // Try to parse the accumulated buffer as JSON
                let updatedOutline = jsonAutocomplete(buffer);
                updatedOutline = updatedOutline
                    .replace(/json/g, "")
                    .replace(/```/g, "")
                    .replaceAll("\n", "");  // Remove any unnecessary newlines

                // Update contentOutline with the latest parsed data
                contentOutline.value = JSON.parse(updatedOutline);

                // Check if content_outline.content is a string, and parse it if necessary
                if (typeof contentOutline.value.content_outline?.content === 'string') {
                    // Attempt to parse content if it looks like JSON
                    try {
                        contentOutline.value.content_outline.content = JSON.parse(contentOutline.value.content_outline.content);
                    } catch (error) {
                        console.log("Content is not valid JSON:", error);
                    }
                }

                // Update the final content dynamically from the stream
                content.value =
                    contentOutline.value.content_outline_stream?.content ||
                    contentOutline.value.content_outline?.content || "";

                // Update raw content output
                rawContent.value = buffer;  // Show the raw JSON as it's streaming in
            } catch (error) {
                // If JSON is incomplete, keep buffering until it's complete
                console.log("Incomplete JSON, buffering more data...");
            }
        }
    } catch (error) {
        console.error("Error fetching content outline:", error);
    }
}

// Fetch content outline on component mount
onMounted(() => {
    const routeParams = router.currentRoute.value.params;
    contentOutlineId.value = routeParams.id;
    fetchContentOutline();
});
</script>

<style scoped>
.container {
    max-width: 800px;
    margin: 0 auto;
}

.content-outline p {
    line-height: 1.5;
}
</style>
