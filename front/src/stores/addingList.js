import { ref } from "vue"
import { defineStore } from "pinia"
import axios from '@/utils/apiRequester'

export const useAddingListStore = defineStore('addingList', () => {
    const addingList = ref(null)

    async function getAddingList() {
        try {
            const res = await axios.get('dragged')

            if (res.status === 200 && res.data) {
                addingList.value = res.data
            }
            
        } catch(error) {
            console.error("Error while fetching list in the store :", error)
        }
    }

    return {addingList, getAddingList}
})