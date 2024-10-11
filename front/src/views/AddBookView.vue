<template>
    <div>
        <h3 class="text-lg font-bold text-center">New Book</h3>
        <form @submit.prevent="submit" class="flex flex-col">
            <label id="title">Title</label>
            <SearchFormInput ebook-property="title" required/>

            <label id="author">Author</label>
            <SearchFormInput ebook-property="author" required/>

            <label id="publisher">Publisher</label>
            <SearchFormInput ebook-property="publisher" required/>

            <label id="theme">Themes</label>
            <SearchFormInput ebook-property="theme"/>

            <label id="genre">Genres</label>
            <SearchFormInput ebook-property="genre"/>

            <button class="my-4 btn btn-outline btn-neutral" type="submit">Send</button>
        </form>
    </div>
</template>

<script setup>
import SearchFormInput from '@/components/SearchFormInput.vue';

function submit(event) {
    const elements = event.target.elements
    const ebook = {
        "title" : elements.namedItem("title").value,
        "author" : elements.namedItem("author").value,
        "publisher" : elements.namedItem("publisher").value,
        "theme" : elements.namedItem("theme").value,
        "genre" : elements.namedItem("genre").value
    }
}
</script>