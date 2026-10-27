"use client";
import { Button, LinkButton } from "@/components/ui/button";
import { ErrorState } from "@/components/ui/feedback";

export default function ErrorPage({ reset }: { error: Error & { digest?: string }; reset: () => void }) {
  return (
    <>
      <h1 className="text-page-title">حدث خطأ غير متوقع</h1>
      <ErrorState title="تعذّر عرض هذه الصفحة" body="لم يُفقد شيء من تقدّمك. أعد المحاولة، وإن تكرر الخطأ فأبلِغ عنه." action={<div className="row"><Button variant="primary" onClick={reset}>أعد المحاولة</Button><LinkButton variant="ghost" href="/report">أبلِغ عن مشكلة</LinkButton></div>} />
    </>
  );
}
