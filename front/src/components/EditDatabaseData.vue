<template>
    <dialog id="edit_modal" ref="editModal" class="modal" @key.enter.prevent>
        <div class="modal-box">
            <form @submit.prevent="submit" class="flex flex-col">
                <h1 class="text-center my-10">Edit</h1>
                <label id="title">Title</label>
                <SearchFormInput ebook-property="title" :placeholder="titlePlaceholder" autofocus />

                <label id="author">Author</label>
                <SearchFormInputWithChips ebook-property="author" :placeholder="authorPlaceholder" @updated="(k,v) => updateCommonChips(k, v)" @keydown.enter.prevent/>

                <label id="publisher">Publisher</label>
                <SearchFormInput ebook-property="publisher" :placeholder="publisherPlaceholder" />

                <label id="year_of_publication_label" for="year_of_publication">Year Of Publication</label>
                <input class="input" id="year_of_publication" name="year_of_publication"
                    :placeholder="yearOfPublicationPlaceholder" />

                <label id="theme">Themes</label>
                <SearchFormInputWithChips ebook-property="theme" :placeholder="themePlaceholder" @updated="(k,v) => updateCommonChips(k, v)" @keydown.enter.prevent />

                <label id="genre">Genres</label>
                <SearchFormInputWithChips ebook-property="genre" :placeholder="genrePlaceholder" @updated="(k,v) => updateCommonChips(k, v)" @keydown.enter.prevent />

                <button class="my-4 btn btn-outline btn-neutral" type="submit">Done</button>
                <button class="my-4 btn btn-outline btn-neutral" type="button" onclick="edit_modal.close()">
                    Cancel
                </button>
            </form>
        </div>
    </dialog>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import SearchFormInput from './SearchFormInput.vue'
import SearchFormInputWithChips from './SearchFormInputWithChips.vue';

const emit = defineEmits(['updated']);

const {ebooks} = defineProps({
    ebooks: {
        required: true,
        type: Array
    }
})

const authorPlaceholder = ref(null)
const titlePlaceholder = ref(null)
const yearOfPublicationPlaceholder = ref(null)
const publisherPlaceholder = ref(null)
const genrePlaceholder = ref(null)
const themePlaceholder = ref(null)

onMounted(() => {
    authorPlaceholder.value = getArrayValue('author')
    titlePlaceholder.value = getValue('title')
    yearOfPublicationPlaceholder.value = getNumericValue('year_of_publication')
    publisherPlaceholder.value = getValue('publisher')
    genrePlaceholder.value = getArrayValue('genre')
    themePlaceholder.value = getArrayValue('theme')
})

const chips = ref({
    "author" : [],
    "theme" : [],
    "genre" : []
})


/**
 * The submit function only takes into account fields that have been changed,
 * but lets the parent component, EditableMetadataTable, take care of actually
 * mutating it.
 * @params {Event} event : the form submitted on click
 **/
function submit(event) {
    console.log("submit fired")
    const elements = event.target.elements
    const mapping = {
        "title": titlePlaceholder,
        "author": authorPlaceholder,
        "publisher": publisherPlaceholder,
        "year_of_publication": yearOfPublicationPlaceholder,
        "theme": themePlaceholder,
        "genre": genrePlaceholder
    }

    const guids = ebooks.length === 1 ? [ ebooks[0].ebook_guid ] : ebooks.map((e) => e.ebook_guid)
    const updatedData = {}
    for (const f in mapping) {
        const field = elements.namedItem(f).value
        if (field && field !== mapping[f].value && !["author", "genre", "theme"].includes(f)) {
            if (["title", "publisher"].includes(f)) {
                updatedData[f] = field
            } else if (f === "year_of_publication") {
                updatedData[f] = parseInt(field, 10)
            }
            continue;
        }
        if (["author", "genre", "theme"].includes(f) && chips.value[f].length) {
            updatedData[f] = chips.value[f]
        }
    }

    const updatedBooks = guids.map(v => Object.assign({"ebook_guid" : v}, updatedData))
    // When it comes to the database, 
    // we'll return every book individually so we can edit multiple ebooks then send
    // less modifications in the back. Too bad the request can end up massive.
    emit('updated', updatedBooks)
}

function getValue(ppty) {
    if (ebooks.length === 1) {
        return ebooks[0][ppty]
    }

    let sameValues = ebooks.every((e, i) => ebooks[0][ppty] === ebooks[i][ppty])

    if (sameValues) return ebooks[0][ppty]
    else return "Various"
}

/**
 *
 * Returns either Various or the joint value of common array
 * @param {String} ppty - property to look for in book object
 * @return {String}
 *
 **/
function getArrayValue(ppty){
    if (ebooks.length === 1) {
        return ebooks[0][ppty] ? ebooks[0][ppty].join(', ') : null
    }

    let arrVal = ebooks[0][ppty]
    for (let i = 1; i < ebooks.length; i++) {
        if (ebooks[i].length !== ebooks[0].length) return "Various"

        for (let j = 0; j < ebooks[i].length; j++) {
            if (ebooks[i][j] !== arrVal[j]) {
                return "Various"
            }
        }
    }

    return arrVal ? arrVal.join(', ') : null
}

function getNumericValue(ppty) {
    if (ebooks.length === 1) return ebooks[0][ppty]

    if (ebooks.every((e, i) => ebooks[0][ppty] === e[ppty])) {
        return ebooks[0][ppty]
    } else {
        return "Various"
    }
}

function updateCommonChips(key, val) {
    chips.value[key] = val;
}
</script>

<style></style>
