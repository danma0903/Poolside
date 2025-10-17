import AsyncStorage from "@react-native-async-storage/async-storage";

const storageKeys = {
	STREAMURL: "streamURL",
};

export const storeData = async (value: string) => {
	try {
		await AsyncStorage.setItem(storageKeys.STREAMURL, value);
	} catch (e) {
		// saving error
		console.log("error saving to local storage: ", e);
	}
};

export const getStreamURL = async () => {
	try {
		const value = await AsyncStorage.getItem(storageKeys.STREAMURL);
		if (value !== null) {
			return value;
		} else {
			console.log("streamurl was null");
			return null;
		}
	} catch (e) {
		// error reading value
		console.log("error retrieving value");
	}
};
