import { defineStore } from "pinia";
import { ref } from "vue";
import axios from "../utils/apiRequester";

export const ebookStore = defineStore('ebooks', () => {
    const ebooks = ref(null)

    async function index() {
        let res = await axios.get('ebooks')
        try {
          ebooks.value = res.data
          return ebooks.value | []
        }
        catch (error) {
          console.log(error)
        }

    }
    return { ebooks, index }
}
)