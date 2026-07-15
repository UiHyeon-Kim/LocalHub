import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import PlaceListView from '@/views/PlaceListView.vue'
import PlaceDetailView from '@/views/PlaceDetailView.vue'
import PostListView from '@/views/PostListView.vue'
import PostDetailView from '@/views/PostDetailView.vue'
import PostFormView from '@/views/PostFormView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: HomeView
    },
    {
      path: '/places',
      name: 'PlaceList',
      component: PlaceListView
    },
    {
      path: '/places/:id',
      name: 'PlaceDetail',
      component: PlaceDetailView
    },
    {
      path: '/posts',
      name: 'PostList',
      component: PostListView
    },
    {
      path: '/posts/new',
      name: 'PostCreate',
      component: PostFormView
    },
    {
      path: '/posts/:id',
      name: 'PostDetail',
      component: PostDetailView
    },
    {
      path: '/posts/:id/edit',
      name: 'PostEdit',
      component: PostFormView
    }
  ]
})

export default router