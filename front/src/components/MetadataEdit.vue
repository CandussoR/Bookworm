<template>
    <dialog id="edit_modal" ref="editModal" class="modal">
        <div class="modal-box">
            <form @submit.prevent="submit" class="flex flex-col">
                <h1 class="text-center my-10">Edit</h1>
                <label id="title">Title</label>
                <SearchFormInput ebook-property="title" :placeholder="titlePlaceholder" autofocus />

                <label id="author">Author</label>
                <SearchFormInput ebook-property="author" :placeholder="authorPlaceholder" />

                <label id="publisher">Publisher</label>
                <SearchFormInput ebook-property="publisher" :placeholder="publisherPlaceholder" />

                <label id="year_of_publication_label" for="year_of_publication">Year Of Publication</label>
                <input class="input" id="year_of_publication" name="year_of_publication"
                    :placeholder="yearOfPublicationPlaceholder" />

                <label id="theme">Themes</label>
                <SearchFormInput ebook-property="theme" :placeholder="themePlaceholder" />

                <label id="genre">Genres</label>
                <SearchFormInput ebook-property="genre" :placeholder="genrePlaceholder" />

                <button class="my-4 btn btn-outline btn-neutral" type="submit">Done</button>
                <button class="my-4 btn btn-outline btn-neutral" type="button" onclick="edit_modal.close()">
                    Cancel
                </button>
            </form>
        </div>
    </dialog>
</template>

<script setup>
import { computed } from 'vue';
import SearchFormInput from './SearchFormInput.vue'

const emit = defineEmits(['updated']);

const props = defineProps({
    ebooks: {
        required: true,
        type: Object
    },
    keys: {
        required: true,
        type: Array
    }
})

// Needs testing
// Those are not reactive, so they can make for a quick comparison with input
// to determine if the input is dirty or not.
const authorPlaceholder = computed(() => getArrayValue('author'))
const titlePlaceholder = computed(() => getValue('title'))
const yearOfPublicationPlaceholder = computed(() => getNumericValue('year_of_publication'))
const publisherPlaceholder = computed(() => getValue('publisher'))
const genrePlaceholder = computed(() => getArrayValue('genre'))
const themePlaceholder = computed(() => getArrayValue('theme'))

console.table([authorPlaceholder, titlePlaceholder, yearOfPublicationPlaceholder, publisherPlaceholder, genrePlaceholder, themePlaceholder])

// Needs Testing
/**
 * The submit function only takes into account fields that have been changed,
 * but lets the parent component, EditableMetadataTable, take care of actually
 * mutating it.
 * @params {Event} event : the form submitted on click
 **/
function submit(event) {
    const elements = event.target.elements
    const mapping = {
        "title": titlePlaceholder,
        "author": authorPlaceholder,
        "publisher": publisherPlaceholder,
        "year_of_publication": yearOfPublicationPlaceholder,
        "theme": themePlaceholder,
        "genre": genrePlaceholder
    }

    const updates = {
        "filepath" :  props.keys.length === 1 ? props.keys[0] : props.keys,
        "metadata" : {}
    }

    for (const f in mapping) {
        const field = elements.namedItem(f).value
        if (field && field !== mapping[f].value) {
            if (["author", "genre", "theme"].includes(f)) {
                updates["metadata"][f] = [field]
            } else if (["title", "publisher"].includes(f)) {
                updates["metadata"][f] = field
            } else if (f === "year_of_publication") {
                updates["metadata"][f] = parseInt(field, 10)
            }
        }
    }

    emit('updated', updates)
}

function getValue(ppty) {
    if (props.keys.length === 1)
        return ppty in props.ebooks[props.keys[0]] ? props.ebooks[props.keys[0]][ppty] : ''

    let returnValue = null

    for (let i = 0; i < props.keys.length; i++) {
        const k = props.keys[i]
        const isProp = ppty in props.ebooks[k]

        if (isProp) {
            if (returnValue === null) {
                returnValue = props.ebooks[k][ppty]
                continue;
            }
            if (returnValue === '' || returnValue !== props.ebooks[k][ppty]) {
                return 'Various'
            }
        }

        if (returnValue) {
            return "Various"
        }
        if (returnValue === null) {
            returnValue = ''
        }
    }
    return returnValue
}

/**
 *
 * Returns either Various or the joint value of common array
 * @param {String} ppty - property to look for in book object
 * @return {String}
 *
 **/
function getArrayValue(ppty) {
    console.log(props.keys.length === 1)
    if (props.keys.length === 1) {
        try {
            return ppty in props.ebooks[props.keys[0]] ? props.ebooks[props.keys[0]][ppty].join(', ') : ''
        } catch (error) {
            console.warn(
                'Erreur au chargement du tableau',
                ppty,
                props.ebooks[props.keys[0]],
                props.keys,
                props.ebooks[props.keys[0]],
                props.ebooks[props.keys[0]][ppty]
            )
            return
        }
    }

    let arrVal = []
    for (let i = 0; i < props.keys.length; i++) {
        const k = props.keys[i]
        if (!(ppty in props.ebooks[k])) {
            continue
        } else if (!arrVal.length) {
            arrVal = props.ebooks[k][ppty]
            continue
        } else if (props.ebooks[k][ppty].length !== arrVal.length) {
            return 'Various'
        }

        for (let j = 0; j < props.ebooks[k][ppty].length; j++) {
            if (props.ebooks[k][ppty][j] !== arrVal[j]) {
                return 'Various'
            }
        }
    }
    return typeof arrVal === 'object' ? arrVal.join(', ') : arrVal
}

function getNumericValue(ppty) {
    if (props.keys.length === 1) return ppty in props.ebooks[props.keys[0]] ? props.ebooks[props.keys[0]][ppty] : null

    let yOp = null
    for (const ebook in props.ebooks) {
        const isProp = ppty in props.ebooks[ebook]
        if (!isProp) {
            if (yOp === 0) {
                continue; 
            }
            if (yOp === null) {
                // Just changing value to signal we've been there
                yOp = 0
                continue
            } 
            if (yOp) {
                return "Various"
            }
        }

        if (yOp === 0 || yOp !== props.ebooks[ebook]) {
            return "Various"
        }
        yOp = props.ebooks[ebook]
    }

    return yOp
}
</script>

<style></style>
