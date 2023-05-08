import jwtService from "@/services/jwt.service";

export const types = {
    SET_AUTH: "SET_AUTH",
    SET_ERROR: "SET_ERROR",
    PURGE_AUTH: "PURGE_AUTH",
}
export default {
    [types.SET_AUTH]: (state, user) => {
        if (user.user) {
            state.isAutheticated = true;
            state.user = user.user;
        } else {
            state.user = user;
        }
        state.errors = {};
        if (user.access_token) {
            jwtService.setToken(user.access_token);
        } else {
            state.isAutheticated = !!jwtService.getToken();
        }
    },
    [types.SET_ERROR]: (state, error) => {
        state.errors = error;
    },
    [types.PURGE_AUTH]: (state) => {
        state.isAutheticated = false;
        state.user = {};
        state.errors = {};
        jwtService.destroyToken();
    }
};