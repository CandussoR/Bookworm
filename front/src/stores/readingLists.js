import { defineStore } from "pinia";
import { ref } from "vue";
import axios from '../utils/apiRequester';

export const useReadingListStore = defineStore('readingLists', () => {
    const readingLists = ref([])

    async function index() {
        try {
            const res = await axios.get('reading_lists')
            if (res.data) {
                readingLists.value = res.data
            }
        }
        catch (error) {
            console.warn(error)
        }
    }

    return {readingLists, index}
})