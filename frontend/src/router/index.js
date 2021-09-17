import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '',
    component: () => import("../layouts/Main.vue"),
    children: [
      {
        path: '/',
        name: 'home',
        component: () => import("../views/Home.vue")
      },
      // {
      //   path: '/dashboard/email_updates',
      //   name: 'email-updates',
      //   component: () => import("../views/Email.vue")
      // },
      {
        path: '/dashboard/:product_uid/:product_token',
        name: 'seller-dashboard',
        component: () => import("../views/SellerDashboard.vue"),
        meta: {
          layout: {
            cols: {
              md: 12
            }
          },
          header: 'sub'
        }
      },
      {
        path: '/product/:product_uid',
        name: 'product',
        component: () => import("../views/Product.vue"),
        meta: {
          header: 'sub'
        }
      },
      {
        path: '/checkout/:order_uid',
        name: 'checkout',
        component: () => import("../views/Checkout.vue"),
        meta: {
          layout: {
            cols: {
              md: 7
            }
          },
          header: 'sub'
        }
      },
      {
        path: '/order/:order_uid',
        name: 'order',
        component: () => import("../views/Order.vue"),
        meta: {
          header: 'sub'
        }
      },
      {
        path: '*',
        name: 'page-404',
        component: () => import("../views/404.vue"),
      }
    ]
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
