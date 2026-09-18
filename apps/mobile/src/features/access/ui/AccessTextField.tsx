import { useState, type Ref } from 'react';
import {
  Pressable,
  StyleSheet,
  Text,
  TextInput,
  View,
  type TextInputProps,
} from 'react-native';

import { accessTheme } from '../theme/accessTheme';
import { AccessFieldError } from './AccessFieldError';

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
  returnKeyType?: TextInputProps['returnKeyType'];
  onBlur?: TextInputProps['onBlur'];
  onSubmitEditing?: TextInputProps['onSubmitEditing'];
  inputRef?: Ref<TextInput>;
  error?: string;
  editable?: boolean;
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
  returnKeyType,
  onBlur,
  onSubmitEditing,
  inputRef,
  error,
  editable = true,
}: AccessTextFieldProps) {
  const [revealed, setRevealed] = useState(false);
  const [focused, setFocused] = useState(false);
  const obscured = secure && !revealed;
  const hasError = error !== undefined;

  return (
    <View style={styles.field}>
      <Text style={styles.label}>{label}</Text>
      <View style={styles.inputWrap}>
        <TextInput
          {...(inputRef === undefined ? {} : { ref: inputRef })}
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
          returnKeyType={returnKeyType}
          editable={editable}
          accessibilityLabel={hasError ? `${label}. ${error}` : label}
          accessibilityState={{ disabled: !editable }}
          onFocus={() => setFocused(true)}
          onBlur={(event) => {
            setFocused(false);
            onBlur?.(event);
          }}
          onSubmitEditing={onSubmitEditing}
          style={[
            styles.input,
            secure ? styles.secureInput : null,
            focused ? styles.inputFocused : null,
            hasError ? styles.inputError : null,
            !editable ? styles.inputDisabled : null,
          ]}
          selectionColor={accessTheme.colors.accent}
        />
        {secure ? (
          <Pressable
            accessibilityRole="button"
            accessibilityLabel={revealed ? hideLabel : showLabel}
            accessibilityState={{ expanded: revealed, disabled: !editable }}
            disabled={!editable}
            hitSlop={8}
            onPress={() => setRevealed((current) => !current)}
            style={({ pressed }) => [
              styles.reveal,
              pressed && editable ? styles.revealPressed : null,
            ]}
          >
            <Text style={styles.revealText}>{revealed ? hideLabel : showLabel}</Text>
          </Pressable>
        ) : null}
      </View>
      {hasError ? <AccessFieldError message={error} /> : null}
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
  inputFocused: {
    borderWidth: 1.5,
    borderColor: accessTheme.colors.ink,
  },
  inputError: {
    borderWidth: 1.5,
    borderColor: accessTheme.colors.accentText,
  },
  inputDisabled: {
    opacity: 0.64,
  },
  secureInput: {
    paddingRight: 118,
  },
  reveal: {
    position: 'absolute',
    top: 4,
    right: 4,
    minWidth: 104,
    minHeight: 44,
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: 10,
    paddingHorizontal: 10,
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
