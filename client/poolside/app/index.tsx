import { Text, TextInput, View, StyleSheet } from "react-native";
import { storeData, getStreamURL } from "@/utils/localStorage";
import { useEffect, useState } from "react";
import { NativeStackNavigationProp } from "@react-navigation/native-stack";
import { Router, useRouter } from "expo-router";
import {
	NativeSyntheticEvent,
	TextInputSubmitEditingEventData,
} from "react-native";

export default function Index() {
	const router = useRouter();
	const [text, setText] = useState<string>();

	//not working
	useEffect(() => {
		const loadPreviousURL = async () => {
			try {
				const existingUrl = await getStreamURL();

				if (existingUrl) {
					setText(existingUrl);
				} else {
					setText("");
				}
			} catch (e) {
				console.log(e);
			}
		};
		loadPreviousURL();
	}, []);

	//grab url, if it is null text is undefined.
	return (
		<View
			style={{
				flex: 1,
				justifyContent: "center",
				alignItems: "center",
			}}
		>
			<TextInput
				style={styles.inputBox}
				placeholder="type your RTSP/ stream URL"
				onSubmitEditing={(event) => handleRTSPInput(event, router)}
			></TextInput>
			{/* <Text>Edit app/index.tsx to edit this screen.</Text> */}
		</View>
	);
}

const handleRTSPInput = async (
	event: NativeSyntheticEvent<TextInputSubmitEditingEventData>,
	router: Router
) => {
	await storeData(event.nativeEvent.text);
	if (event.nativeEvent.text) router.push("./video-preview");
};

const styles = StyleSheet.create({
	inputBox: {
		backgroundColor: "gray",
		borderColor: "black",
		borderWidth: 1,
		borderRadius: 10,
		paddingLeft: 10,
		paddingRight: 10,
		height: 50,
		width: 200,
		fontSize: 12,
	},
});
