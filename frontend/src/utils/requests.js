import axios from "axios";

import { homeAPI, gameAPI, playersAPI, playerAPI, playerEventsAPI, eventAPI } from "./urls";
import { alertError, showFailureNotification } from "./utils";

const instance = axios.create({
  headers: { "Content-Type": "application/json" },
});

// Need to test returning response.json() vs response.data

/**
 * Object representing a Player
 * @typedef {Object} Player
 * @property {string} id
 * @property {string} game_id
 * @property {string} name
 * @property {number} score
 * @property {number} streak
 * @property {string} api
 * @property {Event[]} events - List of all event IDs
 */

/**
 * Object representing an Event
 * @typedef {Object} Event
 * @property {string} id
 * @property {string} player_id
 * @property {string} query
 * @property {number} difficulty - "0" for warmup, 1 for round 1, etc.
 * @property {number} points_gained - +ve / -ve point difference
 * @property {NO_RESPONSE/WRONG/CORRECT} response_type
 * @property {RFC3339} timestamp
 */

/**
 * Object representing a Game
 * @typedef {Object} Game
 * @property {string} id
 * @property {number} round
 * @property {playerId[]} players - List of player IDs
 * @property {boolean} paused
 */

// Main page requests - ("/api")

/**
 * Fetches all games
 * @async
 * @return {Promise<{gameId: Game, ...}>} Object containing all Game objects
 */
export async function fetchAllGames() {
  try {
    const response = await instance.get(homeAPI());
    return response.data;
  } catch (error) {
    alertError(error);
  }
}

/**
 * Creates a new game and returns its game JSON object
 * @async
 * @return {Promise<Game>} Game object of newly created game
 */
export async function createNewGame() {
  try {
    const response = await instance.post(homeAPI());
    return response.data;
  } catch (error) {
    alertError(error);
  }
}

/**
 * Drops all games, ids, events
 * @async
 * @return unsure
 */
export async function deleteAllGames() {
  try {
    const response = await instance.delete(homeAPI());
    return response.data;
  } catch (error) {
    alertError(error);
  }
}

// Requests to "/api/(gameId)"

/**
 * Fetches game JSON object for a given game ID
 * @async
 * @param  {string} gameId
 * @return {Promise<Game>} Game JSON object
 */
export async function fetchGame(gameId) {
  try {
    const response = await instance.get(gameAPI(gameId));
    return response.data;
  } catch (error) {
    alertError(error);
  }
}

/**
 * Updates game by either updating the round, or by pausing/unpausing the game
 *
 * Sending an object containing {"round": roundNum} will advance the game to roundNum
 * Sending an object containing {"pause": (true|false)} will pause the game if true and unpause if false
 * @async
 * @param  {string} gameId
 * @param  {{"round": number, "pause": boolean}} data Object containing either the round or whether to pause/unpause
 * @return {Promise<string>} unsure
 */
export async function updateGame(gameId, data) {
  try {
    const response = await instance.put(gameAPI(gameId, data));
    return response.data;
  } catch (error) {
    alertError(error);
  }
}

/**
 * Drops a given game
 * @async
 * @param  {string} gameId
 * @return {Promise<{"deleted": gameId}>} Id of deleted game
 */
export async function deleteGame(gameId) {
  try {
    const response = await instance.delete(gameAPI(gameId));
    return response.data;
  } catch (error) {
    alertError(error);
  }
}

// Requests to "/api/(game_id)/players"

/**
 * Fetches all players in a given game
 * @async
 * @param  {string} gameId
 * @return {Promise<Player[]>} List of all player JSON objects
 */
export async function fetchAllPlayers(gameId) {
  try {
    const response = await instance.get(playersAPI(gameId));
    return response.data.players;
  } catch (error) {
    alertError(error);
  }
}

/**
 * Validates user submission and creates new player if valid
 * @async
 * @param  {string} gameId
 * @param  {string} name   Name submitted by user
 * @param  {string} api    URL submitted by user
 * @return {Promise<Player>}        Player JSON object for newly created player (returns false if invalid)
 */
export async function createPlayer(gameId, name, api) {
  const valid = await validateData(gameId, { name: name, api: api });

  if (!valid) {
    console.error("Invalid data submitted");
    throw "Invalid data submitted"
  }

  const playerData = {
    name: name.trim(),
    api: api,
  };

  try {
    const response = await instance.post(playersAPI(gameId), playerData);
    return response.data;
  } catch (error) {
    alertError(error);
  }
}

/**
 * Validates a given name and api url
 * @async
 * @param {string} gameId
 * @param {{"name": string, "api": string}} data Object containing name and/or api
 * @returns {Promise<boolean>} Returns true if valid and false if invalid
 */
async function validateData(gameId, data) {
  // Check gameId exists
  try {
    const response = await fetchGame(gameId);
    // console.log(response);
  } catch (error) {
    showFailureNotification("Error creating player", "Game id does not exist!");
    return false;
  }

  const players = await fetchAllPlayers(gameId);

  if (data.name) {
    const name = data.name.trim();

    // Check player name is not empty
    if (name === "") {
      showFailureNotification("Error creating player", "Your name cannot be empty!");
      return false;
    }

    // Check player name is unique in a game
    const names = players.map((player) => {
      player.name;
    });

    if (name in names) {
      showFailureNotification("Error creating player", "Your name already exists in the game!");
      return false;
    }
  }

  if (data.api) {
    // Check valid URL
    if (data.api.substring(0, 7) !== "http://" && data.api.substring(0, 8) !== "https://") {
      showFailureNotification("Error creating player", "You entered an invalid URL!");
      return false;
    }

    // Check api url is unique in a game
    const apis = players.map((player) => {
      player.api;
    });

    if (data.api in apis) {
      showFailureNotification("Error creating player", "Your url already exists in the game!");
      return false;
    }
  }

  return true;
}

/**
 * Deletes all players in a game
 * @param  {string} gameId
 * @return unsure
 */
export async function deleteAllPlayers(gameId) {
  try {
    const response = await instance.delete(playersAPI(gameId));
    return response.data;
  } catch (error) {
    alertError(error);
  }
}

// Requests to "/api/(game_id)/players/(player_id)"

/**
 * Returns player JSON object for a given player in a given game
 * @async
 * @param  {string} gameId
 * @param  {string} playerId
 * @return {Promise<Player>} Player JSON object
 */
export async function fetchPlayer(gameId, playerId) {
  try {
    const response = await instance.get(playerAPI(gameId, playerId));
    return response.data;
  } catch (error) {
    alertError(error);
  }
}

/**
 * Updates a player's name and/or api url
 * @async
 * @param  {string} gameId
 * @param  {string} playerId
 * @param  {{name: string, api: string}} data Object containing new name and/or new api
 * @return {Promise<Player>} Updated player JSON object (returns false if data is invalid)
 */
export async function updatePlayer(gameId, playerId, data) {
  const valid = await validateData(gameId, data);

  if (!valid) {
    console.error("Invalid data submitted");
    return false;
  }

  try {
    const response = await instance.put(playerAPI(gameId, playerId), data);
    return response.data;
  } catch (error) {
    alertError(error);
  }
}

/**
 * Drops a player
 * @async
 * @param  {string} gameId
 * @param  {string} playerId
 * @return {Promise<{"deleted": playerId}>} ID of the deleted player
 */
export async function deletePlayer(gameId, playerId) {
  try {
    const response = await instance.delete(playerAPI(gameId, playerId));
    return response.data;
  } catch (error) {
    alertError(error);
  }
}

// "/api/(game_id)/players/(player_id)/events"

/**
 * Returns a list of all event JSON objects for a given player
 * @async
 * @param  {string} gameId
 * @param  {string} playerId
 * @return {Promise<Event[]>} List of all event JSON objects
 */
export async function fetchAllEvents(gameId, playerId) {
  try {
    const response = await instance.get(playerEventsAPI(gameId, playerId));
    return response.data.events;
  } catch (error) {
    alertError(error);
  }
}

/**
 * Deletes all events for a given player
 * @async
 * @param  {string} gameId
 * @param  {string} playerId
 * @return unsure
 */
export async function deleteAllEvents(gameId, playerId) {
  try {
    const response = await instance.delete(playerEventsAPI(gameId, playerId));
    return response.data;
  } catch (error) {
    alertError(error);
  }
}

// "/api/(game_id)/players/(player_id)/events/(event_id)"

/**
 * Returns the event JSON object for a given eventId
 * @async
 * @param  {string} gameId
 * @param  {string} playerId
 * @param  {string} eventId
 * @return {Promise<Event>} Event JSON object
 */
export async function fetchEvent(gameId, playerId, eventId) {
  try {
    const response = await instance.get(eventAPI(gameId, playerId, eventId));
    return response.data;
  } catch (error) {
    alertError(error);
  }
}

/**
 * Drops a given event
 * @async
 * @param  {string} gameId
 * @param  {string} playerId
 * @param  {string} eventId
 * @return {Promise<{"deleted": eventId}>} ID of deleted event
 */
export async function deleteEvent(gameId, playerId, eventId) {
  try {
    const response = await instance.delete(eventAPI(gameId, playerId, eventId));
    return response.data;
  } catch (error) {
    alertError(error);
  }
}
