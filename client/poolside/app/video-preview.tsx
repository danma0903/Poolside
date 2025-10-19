import React, { useState, useEffect } from "react";
import { View, Image, StyleSheet, Text, ImageBackground } from "react-native";
import AlertBox from "@/components/AlertBox";

export default function VideoPreview() {
	const [frameUri, setFrameUri] = useState<string | null>(null);

	useEffect(() => {
		const ws = new WebSocket("ws://10.113.114.118:8888");

		
		ws.onopen = () => console.log("✅ WebSocket connected");

		ws.onmessage = (event) => {
			const base64Data = event.data as string;

			// 1️⃣ Convert Base64 into Data URI
			const dataUri = `data:image/jpeg;base64,${base64Data}`;

			// 2️⃣ Update state to render the frame
			setFrameUri(dataUri);
		};

		ws.onclose = () => console.log("❌ WebSocket closed");

		return () => ws.close();
	}, []);

<<<<<<< HEAD
	return (
		<View style={styles.container}>
			<View style={styles.videoWrapper}>
				{frameUri ? (
					<ImageBackground
						source={{ uri: frameUri }}
						style={styles.image}
						resizeMode="cover" // fill the container completely
					>
						<AlertBox />
					</ImageBackground>
				) : (
					<Text>Waiting for video...</Text>
				)}
			</View>
		</View>

	);
}

const styles = StyleSheet.create({
	container: { flex: 1, alignItems: "center", justifyContent: "center" },
	videoWrapper: {
		position: "relative",
		width: 300,
		height: 200,
	},
	image: {
		width: "100%",
		height: "100%",
	},
	alertOverlay: {
		position: "absolute",
		top: 5,
		left: 5,
		backgroundColor: "rgba(255,0,0,0.7)",
		paddingHorizontal: 8,
		paddingVertical: 4,
		borderRadius: 4,
	},
=======
  return (
    <View style={styles.screen}>
      <AlertBox />
      <Text style={styles.title}>Poolside Live Feed</Text>
      <View style={styles.videoContainer}>
        {frameUri ? (
          <Image
            source={{ uri: frameUri }}
            style={styles.image}
            resizeMode="cover"
          />
        ) : (
          <Text style={styles.waitingText}>Waiting for video...</Text>
        )}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: "#3c7e98ff", // light blue background
    alignItems: "center",
    justifyContent: "flex-start",
    paddingTop: 40,
  },
  title: {
    fontSize: 24,
    fontWeight: "700",
    color: "#8cd0fdff", // deeper blue for headings
    marginBottom: 20,
  },
  videoContainer: {
    width: "90%",
    aspectRatio: 16 / 9,
    backgroundColor: "#FFFFFF",
    borderRadius: 15,
    overflow: "hidden",
    alignItems: "center",
    justifyContent: "center",
    shadowColor: "#000",
    shadowOpacity: 0.1,
    shadowRadius: 10,
    shadowOffset: { width: 0, height: 5 },
    elevation: 5,
  },
  image: {
    width: "100%",
    height: "100%",
    borderRadius: 15,
  },
  waitingText: {
    color: "#8cd0fdff",
    fontSize: 16,
    fontWeight: "500",
  },
>>>>>>> cb881d1 (temporary display for video screen)
});
