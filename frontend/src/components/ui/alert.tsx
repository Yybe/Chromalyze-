import React from 'react';

export interface AlertProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'destructive';
}

export const Alert = React.forwardRef<HTMLDivElement, AlertProps>(({ className, variant, ...props }, ref) => {
  return (
    <div
      ref={ref}
      className={`alert ${variant === 'destructive' ? 'alert-destructive' : ''} ${className}`}
      {...props}
    />
  );
});
Alert.displayName = 'Alert';

export interface AlertTitleProps extends React.HTMLAttributes<HTMLHeadingElement> {}

export const AlertTitle = React.forwardRef<HTMLHeadingElement, AlertTitleProps>(({ className, ...props }, ref) => {
  return <h3 ref={ref} className={`alert-title ${className}`} {...props} />;
});
AlertTitle.displayName = 'AlertTitle';

export interface AlertDescriptionProps extends React.HTMLAttributes<HTMLParagraphElement> {}

export const AlertDescription = React.forwardRef<HTMLParagraphElement, AlertDescriptionProps>(({ className, ...props }, ref) => {
  return <p ref={ref} className={`alert-description ${className}`} {...props} />;
});
AlertDescription.displayName = 'AlertDescription';