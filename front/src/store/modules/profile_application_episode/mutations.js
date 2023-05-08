export const types = {
    SET_PROFILE_APPLICATION_EPISODES: "SET_PROFILE_APPLICATION_EPISODES",
    CLEAR_PROFILE_APPLICATION_EPISODES: "CLEAR_RPOFILE_APPLICATION_EPISODES",
}
export default {
    [types.SET_PROFILE_APPLICATION_EPISODES]: (state, episodes) => {
        state.profile_application_episodes = episodes;
    },
    [types.CLEAR_PROFILE_APPLICATION_EPISODES]: (state) => {
        state.profile_application_episodes = [];
    }
};