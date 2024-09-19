<template>
    <ul v-if="readingLists">
        <li class="hover:cursor-pointer hover:bg-base-100 my-2" v-for="rl in readingLists" :key="rl.reading_list_guid"
            @click="displayList(rl.reading_list_guid)">
            {{ rl.name }}
        </li>
    </ul>
    <div v-else>
        <p>No reading list yet...</p>
    </div>
    <!-- DaisyUI modal -->
    <button class="btn" onclick="my_modal.showModal()">New reading list</button>
    <dialog id="my_modal" ref="myModal" class="modal">
        <div class="modal-box">
            <h3 class="text-lg font-bold">Hello!</h3>
            <p class="py-4">Press ESC key or click the button below to close</p>
            <div class="modal-action">
                <form @submit="submitForm" method="dialog">
                    <label for="name">Name : </label>
                    <input id="name" type="text" v-model="newReadingListName" required minlength="1">
                    <!-- if there is a button in form, it will close the modal -->
                    <button class="btn" type="submit" :disabled="nameValidation ? false : true">Submit</button>
                </form>
            </div>
        </div>
    </dialog>
</template>


<script setup>
import { useReadingListStore } from '@/stores/readingLists';
import { computed, onMounted, ref, useTemplateRef } from 'vue';
import { useRouter } from 'vue-router';
import axios from '../utils/apiRequester';

const router = useRouter();
const store = useReadingListStore();
let readingLists = ref([]);
let newReadingListName = ref('');
let myModal = useTemplateRef('myModal');
let nameValidation = computed(() => newReadingListName.value.length > 1 && !store.readingLists.map(rl => rl.name).includes(newReadingListName.value))
onMounted(async () => {
    try {
        // store.index()
        // if (store.readingLists) {
        //     readingLists.value = readingLists
        // }
        // if (res.data) readingLists.value = res.data
        readingLists.value = [
            {
                "name" : "Fake RL",
                "items": [],
                "reading_list_guid": "GUID-1"
            },
            {
                "name" : "FAKE RL 2",
                "items" : [],
                "reading_list_guid" : "GUID-2"
            }
        ]
    }
    catch (error) {
        console.error(error)
    }
})


function displayList(guid) {
    router.push({name: 'readingLists', params : {'guid' : guid}}); 
}


async function submitForm() {
    if (newReadingListName.value.length > 1 && !store.readingLists.map(rl => rl.name).includes(newReadingListName.value)) {
        let res = await axios.post('reading_lists', {
            "name": newReadingListName.value,
            "description": null,
            "items": null
        })
        if (res.data) {
            store.readingLists.push(res.data);
            router.push('readingList', {params: {'guid': res.data.reading_list_guid}});
        }
    }
}

</script>


<style scoped>

</style>