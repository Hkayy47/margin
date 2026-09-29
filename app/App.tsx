import { StatusBar } from 'expo-status-bar';
import { useEffect, useState } from 'react';
import { Pressable, StyleSheet, Text, View } from 'react-native';
import {
  Camera,
  CommonResolutions,
  useCameraPermission,
  usePhotoOutput,
} from 'react-native-vision-camera';

// M0 "hello camera": live preview plus one button that takes a full-resolution still.
// In M2 the still gets warped, cropped to the finished line and sent to the reader.
export default function App() {
  const { hasPermission, canRequestPermission, requestPermission } = useCameraPermission();
  const photoOutput = usePhotoOutput({
    targetResolution: CommonResolutions.UHD_4_3,
    qualityPrioritization: 'quality',
  });
  const [status, setStatus] = useState('Point the phone at your paper, then tap Check.');
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    if (canRequestPermission) requestPermission();
  }, [canRequestPermission, requestPermission]);

  async function check() {
    setBusy(true);
    const started = Date.now();
    try {
      const photo = await photoOutput.capturePhoto({ enableShutterSound: false }, {});
      const path = await photo.saveToTemporaryFileAsync();
      setStatus(`Still: ${photo.width}×${photo.height} in ${Date.now() - started} ms\n${path}`);
      photo.dispose();
    } catch (e) {
      setStatus(`Capture failed: ${e instanceof Error ? e.message : String(e)}`);
    } finally {
      setBusy(false);
    }
  }

  if (!hasPermission) {
    return (
      <View style={styles.center}>
        <Text style={styles.text}>
          Margin needs the camera to see your paper.
          {canRequestPermission ? '' : '\nTurn it on in Settings → Apps → Margin → Permissions.'}
        </Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Camera style={StyleSheet.absoluteFill} device="back" isActive outputs={[photoOutput]} />
      <View style={styles.bar}>
        <Text style={styles.text}>{status}</Text>
        <Pressable
          style={[styles.button, busy && styles.buttonBusy]}
          onPress={check}
          disabled={busy}
        >
          <Text style={styles.buttonText}>{busy ? '…' : 'Check'}</Text>
        </Pressable>
      </View>
      <StatusBar style="light" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#000' },
  center: { flex: 1, backgroundColor: '#000', alignItems: 'center', justifyContent: 'center', padding: 24 },
  bar: {
    position: 'absolute',
    left: 0,
    right: 0,
    bottom: 0,
    padding: 16,
    paddingBottom: 40,
    gap: 12,
    backgroundColor: 'rgba(0,0,0,0.6)',
  },
  text: { color: '#fff', fontSize: 14, textAlign: 'center' },
  button: { alignSelf: 'center', backgroundColor: '#fff', borderRadius: 32, paddingHorizontal: 40, paddingVertical: 14 },
  buttonBusy: { opacity: 0.5 },
  buttonText: { fontSize: 18, fontWeight: '600', color: '#000' },
});
