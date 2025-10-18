import {
	Text,
	TextInput,
	View,
	StyleSheet,
	NativeSyntheticEvent,
	TextInputSubmitEditingEventData,
	Animated,
} from "react-native";
import { storeData, getStreamURL } from "@/utils/localStorage";
import { useEffect, useState, useRef } from "react";
import { NativeStackNavigationProp } from "@react-navigation/native-stack";
import { Router, useRouter } from "expo-router";

export default function Index() {
	const router = useRouter();
	const [text, setText] = useState<string>();
	const [isLoaded, setIsLoaded] = useState<boolean>(false);

	//page fade animation values
	const fadeInAnim = useRef(new Animated.Value(0)).current;
	// const fadeOutAnim = useRef(new Animated.Value(1)).current;
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
			} finally {
				setIsLoaded(true);
			}
		};
		loadPreviousURL();
	}, []);

	useEffect(() => {
		if (isLoaded) {
			Animated.timing(fadeInAnim, {
				toValue: 1,
				duration: 1000,
				useNativeDriver: true,
			}).start();
		}
	}, [isLoaded, fadeInAnim]);

	if (isLoaded) {
		//grab url, if it is null text is undefined.
		return (
			<View
				style={{
					flex: 1,
					justifyContent: "center",
					alignItems: "center",
					backgroundColor: "#4A4A4A",
				}}
			>
				<Animated.View
					style={{
						flex: 1,
						justifyContent: "center",
						alignItems: "center",
						backgroundColor: "#4A4A4A",
						opacity: fadeInAnim,
					}}
				>
					<TextInput
						style={styles.inputBox}
						defaultValue={text}
						placeholder="type your RTSP/ stream URL"
						onSubmitEditing={(event) => handleRTSPInput(event, router)}
					></TextInput>
				</Animated.View>
			</View>
		);
	}

	return (
		<>
			<Text>Loading...</Text>
		</>
	);
}

const handleRTSPInput = async (
	event: NativeSyntheticEvent<TextInputSubmitEditingEventData>,
	router: Router
) => {
	const text = event.nativeEvent.text;
	await storeData(text);
	if (text) router.push("./video-preview");
	//we might want to add here a validator to make sure we actually can establish a connection
	//before navigating to the next route. We might render an error on the page
	//if the user input is an invalid stream address
	//another option is to first route to a loading screen to establisht eh connection and then route
	//to the video preview
};

const styles = StyleSheet.create({
	inputBox: {
		backgroundColor: "#d2d2d2ff",
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
