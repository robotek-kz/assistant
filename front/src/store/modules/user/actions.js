import ApiService from "@/services/api.service"
import jwtService from "@/services/jwt.service";
import { types } from './mutations';
const api = new ApiService('Это я исправлю попозже');
export default {
    register: async({commit}, credentials) => {
        const data = await api.post('/users', credentials);
        if (!data.ok) {
            const body = await data.body;
            commit(types.SET_ERROR, body.errors.json);
            return false;
        };
        return data;
    },
    login: async({commit}, credentials) => {
        const data = await api.login(credentials.nickname, credentials.password);
        if (data === 'fail') {
            commit(types.SET_ERROR, { error: 'Никнейм или пароль неверный'});
            return false;
        }
        const body = await data.body;
        commit(types.SET_AUTH, body);
        return data;
    },
    checkAuth: async({commit}) => {
        if (jwtService.getToken()) {
            const nickname = await api.get('/me');
            const body = await nickname.body;
            commit(types.SET_AUTH, body);
        } else {
            commit(types.PURGE_AUTH);
        }
    },
    logout: ({commit}) => {
        commit(types.PURGE_AUTH);
    }
};