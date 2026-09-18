import { useRef, useState } from 'react';
import { StyleSheet, Text, TextInput, View } from 'react-native';

import {
  normalizeVerificationCode,
  VERIFICATION_CODE_LENGTH,
} from '../model/signUpFlow';
import { accessTheme } from '../theme/accessTheme';
import { AccessFieldError } from './AccessFieldError';

type AccessOtpFieldProps = Readonly<{
  label: string;
  value: string;
  onChangeText: (value: string) => void;
  error?: string;
  editable?: boolean;
  onSubmitEditing?: () => void;
}>;

const SLOT_INDEXES = Array.from(
  { length: VERIFICATION_CODE_LENGTH },
  (_, index) => index,
);

export function AccessOtpField({
  label,
  value,
  onChangeText,
  error,
  editable = true,
  onSubmitEditing,
}: AccessOtpFieldProps) {
  const inputRef = useRef<TextInput>(null);
  const [focused, setFocused] = useState(false);
  const hasError = error !== undefined;
  const activeIndex = Math.min(value.length, VERIFICATION_CODE_LENGTH - 1);

  function handleChange(nextValue: string) {
    onChangeText(normalizeVerificationCode(nextValue));
  }

  return (
    <View style={styles.field}>
      <Text style={styles.label}>{label}</Text>
      <View style={styles.inputArea}>
        <View
          style={styles.slots}
          pointerEvents="none"
          accessibilityElementsHidden
          importantForAccessibility="no-hide-descendants"
        >
          {SLOT_INDEXES.map((index) => {
            const digit = value[index] ?? '';
            const active = focused && index === activeIndex;

            return (
              <View
                key={index}
                style={[
                  styles.slot,
                  active ? styles.slotFocused : null,
                  hasError ? styles.slotError : null,
                  !editable ? styles.slotDisabled : null,
                ]}
              >
                <Text style={styles.digit}>{digit}</Text>
              </View>
            );
          })}
        </View>

        <TextInput
          ref={inputRef}
          value={value}
          onChangeText={handleChange}
          editable={editable}
          maxLength={VERIFICATION_CODE_LENGTH}
          keyboardType="number-pad"
          autoComplete="one-time-code"
          textContentType="oneTimeCode"
          returnKeyType="done"
          onSubmitEditing={onSubmitEditing}
          onFocus={() => setFocused(true)}
          onBlur={() => setFocused(false)}
          accessibilityLabel={hasError ? `${label}. ${error}` : label}
          accessibilityState={{ disabled: !editable }}
          selectionColor="transparent"
          caretHidden
          style={styles.overlayInput}
        />
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
  inputArea: {
    position: 'relative',
    minHeight: 56,
  },
  slots: {
    flexDirection: 'row',
    gap: 8,
  },
  slot: {
    minWidth: 0,
    height: 56,
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 1,
    borderColor: accessTheme.colors.border,
    borderRadius: 12,
    backgroundColor: accessTheme.colors.surface,
  },
  slotFocused: {
    borderWidth: 1.5,
    borderColor: accessTheme.colors.ink,
  },
  slotError: {
    borderWidth: 1.5,
    borderColor: accessTheme.colors.accentText,
  },
  slotDisabled: {
    opacity: 0.64,
  },
  digit: {
    color: accessTheme.colors.ink,
    fontSize: 22,
    fontWeight: '700',
    fontVariant: ['tabular-nums'],
  },
  overlayInput: {
    position: 'absolute',
    top: 0,
    right: 0,
    bottom: 0,
    left: 0,
    opacity: 0.01,
    color: 'transparent',
    backgroundColor: 'transparent',
  },
});
