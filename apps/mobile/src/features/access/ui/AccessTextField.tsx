import { useState } from 'react';
import {
  Pressable,
  StyleSheet,
  Text,
  TextInput,
  View,
  type TextInputProps,
} from 'react-native';

import { accessTheme } from '../theme/accessTheme';

type AccessTextFieldProps = Readonly<{
  label: string;
  value: string;
  onChangeText: (value: string) => void;
  placeholder?: string;
  secure?: boolean;
  showLabel?: string;
  hideLabel?: string;
  autoComplete?: TextInputProps['autoComplete'];
  keyboardType?: TextInputProps['keyboardType'];
  textContentType?: TextInputProps['textContentType'];
}>;

export function AccessTextField({
  label,
  value,
  onChangeText,
  placeholder,
  secure = false,
  showLabel = 'Show',
  hideLabel = 'Hide',
  autoComplete,
  keyboardType,
  textContentType,
}: AccessTextFieldProps) {
  const [revealed, setRevealed] = useState(false);
  const obscured = secure && !revealed;

  return (
    <View style={styles.field}>
      <Text style={styles.label}>{label}</Text>
      <View style={styles.inputWrap}>
        <TextInput
          value={value}
          onChangeText={onChangeText}
          placeholder={placeholder}
          placeholderTextColor={accessTheme.colors.textMuted}
          secureTextEntry={obscured}
          autoCapitalize="none"
          autoCorrect={false}
          autoComplete={autoComplete}
          keyboardType={keyboardType}
          textContentType={textContentType}
          style={[styles.input, secure ? styles.secureInput : null]}
          selectionColor={accessTheme.colors.accent}
        />
        {secure ? (
          <Pressable
            accessibilityRole="button"
            accessibilityLabel={revealed ? hideLabel : showLabel}
            accessibilityState={{ expanded: revealed }}
            hitSlop={8}
            onPress={() => setRevealed((current) => !current)}
            style={({ pressed }) => [
              styles.reveal,
              pressed ? styles.revealPressed : null,
            ]}
          >
            <Text style={styles.revealText}>{revealed ? hideLabel : showLabel}</Text>
          </Pressable>
        ) : null}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  field: {
    gap: 8,
  },
  label: {
    color: accessTheme.colors.textSecondary,
    fontSize: 13,
    fontWeight: '700',
  },
  inputWrap: {
    position: 'relative',
  },
  input: {
    minHeight: 52,
    borderWidth: 1,
    borderColor: accessTheme.colors.border,
    borderRadius: accessTheme.radii.input,
    backgroundColor: accessTheme.colors.surface,
    color: accessTheme.colors.ink,
    paddingHorizontal: 15,
    fontSize: 16,
  },
  secureInput: {
    paddingRight: 74,
  },
  reveal: {
    position: 'absolute',
    top: 4,
    right: 4,
    minWidth: 62,
    minHeight: 44,
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: 10,
  },
  revealPressed: {
    backgroundColor: accessTheme.colors.surfaceMuted,
  },
  revealText: {
    color: accessTheme.colors.textSecondary,
    fontSize: 12,
    fontWeight: '700',
  },
});
