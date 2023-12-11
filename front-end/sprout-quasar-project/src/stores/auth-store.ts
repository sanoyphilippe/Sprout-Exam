import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token'),
  }),
  getters: {
    getAccessToken: (state) => state.token,
    isUserLoggedIn: (state) => !!state.token
  },
  actions: {
    setUserAccessToken(accessToken: string) {
      localStorage.setItem('token', accessToken);
      this.token = accessToken;
    },

    logoutUser () {
      localStorage.clear();
      this.token = '';
    }
  },
});
