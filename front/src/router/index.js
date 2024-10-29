import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/ebooks/:key/:value',
      name: 'ebooks',
      component: () => import('../views/EbooksView.vue'),
    },
    {
      path: '/authors',
      name: 'authors',
      component: () => import('../views/AuthorsView.vue')
    },
    {
      path: '/readingLists/:guid',
      name: 'readingLists',
      component: () => import('../views/ReadingListView.vue')
    },
    {
      path: '/ebooks/add',
      name: 'newEbook',
      component: () => import('../views/AddBook/AddBookView.vue')
    },
    {
      path: '/ebooks/add/manual',
      name: 'newEbookManual',
      component: () => import('../views/AddBook/AddBookManually.vue')
    },
    {
      path: '/ebooks/add/dragDrop',
      name: 'newEbookDragDrop',
      component: () => import('../views/AddBook/AddBookDragDrop.vue')
    },
    {
      path: '/addingList',
      name: 'addingList',
      component: () => import('../views/AddingListView.vue')
    }
  ]
})

export default router
