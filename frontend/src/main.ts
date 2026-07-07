import { VueQueryPlugin } from "@tanstack/vue-query";
import { createApp } from "vue";
import "@fontsource-variable/inter";
import App from "./App.vue";
import { i18n } from "./i18n";
import "./assets/main.css";

createApp(App).use(i18n).use(VueQueryPlugin).mount("#app");
