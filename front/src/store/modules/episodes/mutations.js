export const types = {
    SET_EPISODES: "SET_EPISODES",
    UPDATE_EPISODES: "UPDATE_EPISODES",
    REMOVE_EPISODES: "REMOVE_EPISODES",
    NEW_EPISODE: "NEW_EPISODE",
    ADD_FILE: "ADD_FILE",
}
export default {
    [types.SET_EPISODES]: (state, episodes) => {
        state.episodes = episodes;
    },
    [types.UPDATE_EPISODES]: (state, episodeUpd) => {
        const index = state.episodes.findIndex(episode => episode.id === episodeUpd.id)
        if (index !== -1) {
            state.episodes.splice(index, 1, episodeUpd);
        }
    },
    [types.REMOVE_EPISODES]: (state, id) => {
        state.episodes = state.episodes.filter(episode => episode.id !== id);
    },
    [types.NEW_EPISODE]: (state, episode) => {
        console.log('mutations episode', episode);
        state.episodes.unshift(episode);
    },
    [types.ADD_FILE]: (state, data) => {
        data.files.map((d) => data.episode.files.push(d))
        const index = state.episodes.findIndex(episode => episode.id === data.episode.id)
        if (index !== -1) {
            state.episodes.splice(index, 1, data.episode);
        }
    }
};