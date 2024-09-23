<template>
    <div class="w-full">
        <div class="w-full">
            <div v-if="contentOutline.content_outline">
                <h1>{{ contentOutline.content_outline.title }}</h1>
                <p>
                    <strong>Target Audience:</strong>
                    {{ contentOutline.content_outline.target_audience }}
                </p>
                <p>
                    <strong>Wrote As:</strong>
                    {{ contentOutline.content_outline.wrote_as }}
                </p>
                <p>
                    <strong>Content:</strong> {{ contentOutline.content_outline.content }}
                </p>

                <hr />

                <div v-if="contentOutline.content_outline.metatags">
                    <p>
                        <strong>URL:</strong>
                        {{ contentOutline.content_outline.metatags.url }}
                    </p>
                    <p>
                        <strong>Page Title:</strong>
                        {{ contentOutline.content_outline.metatags.page_title }}
                    </p>
                    <p>
                        <strong>Page Description:</strong>
                        {{ contentOutline.content_outline.metatags.page_description }}
                    </p>
                </div>

                <pre>{{ contentOutline.content_outline.content }}</pre>
            </div>

            <div v-else>
                <p>No content outline available.</p>
            </div>

            <pre>{{ content }}</pre>
        </div>
    </div>
</template>
<script setup>
import { ref, onMounted, defineProps } from "vue";
import { useRouter } from "vue-router";
import jsonAutocomplete from "json-autocomplete";

const props = defineProps(["contentOutlineId"]);
const router = useRouter();

const contentOutlineId = ref("");
const contentOutline = ref({});
const content = ref("");

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

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = "";

        while (true) {
            const { value, done } = await reader.read();
            if (done) break;
            buffer += decoder.decode(value, { stream: true });

            try {
                let updatedOutline = jsonAutocomplete(buffer);
                updatedOutline = updatedOutline
                    .replace(/json/g, "")
                    .replace(/```/g, "")
                    .replaceAll("\n", "");
                contentOutline.value = JSON.parse(updatedOutline);
                content.value =
                    contentOutline.value.content_outline_stream?.content ||
                    contentOutline.value.content_outline.content;
            } catch (error) {
                console.log("Incomplete JSON, buffering...");
            }
        }
    } catch (error) {
        console.error("Error fetching content outline:", error);
    }
}

onMounted(() => {
    const routeParams = router.currentRoute.value.params;
    contentOutlineId.value = routeParams.id;
    fetchContentOutline();
});
</script>
